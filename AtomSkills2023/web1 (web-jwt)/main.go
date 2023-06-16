package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"github.com/google/uuid"
	"net/http"
	"strings"
	"time"
)

type AuthRequest struct {
	AuthKey string `json:"auth_key"`
}

type HeaderJWT struct {
	Alg string `json:"alg"`
	Typ string `json:"typ"`
}

type PayloadJWT struct {
	Sub   string          `json:"sub"`
	Iat   int64           `json:"iat"`
	Rules RulesPayloadJWT `json:"rules"`
}

type RulesPayloadJWT struct {
	Read  bool `json:"read"`
	Write bool `json:"write"`
}

func signJWT(token string) string {
	h := hmac.New(sha256.New, []byte(""))
	h.Write([]byte(token))

	signature := h.Sum(nil)

	return base64.RawURLEncoding.EncodeToString(signature)
}

func generateJWT() string {
	header := HeaderJWT{
		Alg: "HS256",
		Typ: "JWT",
	}

	payload := PayloadJWT{
		Sub: uuid.New().String(),
		Iat: time.Now().Unix(),
		Rules: RulesPayloadJWT{
			Read:  false,
			Write: false,
		},
	}

	headerJSON, _ := json.Marshal(header)
	payloadJSON, _ := json.Marshal(payload)

	headerBase64 := base64.RawURLEncoding.EncodeToString(headerJSON)
	payloadBase64 := base64.RawURLEncoding.EncodeToString(payloadJSON)

	token := fmt.Sprintf("%s.%s", headerBase64, payloadBase64)
	signature := signJWT(token)

	return fmt.Sprintf("%s.%s", token, signature)
}

func verifyJWT(token string) *PayloadJWT {
	parts := strings.Split(token, ".")
	if len(parts) != 3 {
		return nil
	}

	headerBase64 := parts[0]
	headerJSON, err := base64.RawURLEncoding.DecodeString(headerBase64)
	if err != nil {
		return nil
	}

	var header HeaderJWT
	err = json.Unmarshal(headerJSON, &header)
	if err != nil {
		return nil
	}

	payloadBase64 := parts[1]
	payloadJSON, err := base64.RawURLEncoding.DecodeString(payloadBase64)
	if err != nil {
		return nil
	}

	var payload PayloadJWT
	err = json.Unmarshal(payloadJSON, &payload)
	if err != nil {
		return nil
	}

	if header.Alg != "HS256" {
		return nil
	}

	if header.Typ != "JWT" {
		return nil
	}

	expectedSignature := signJWT(fmt.Sprintf("%s.%s", headerBase64, payloadBase64))

	if hmac.Equal([]byte(parts[2]), []byte(expectedSignature)) {
		return &payload
	} else {
		return nil
	}
}

func setAuthCookie(w http.ResponseWriter, r *http.Request) bool {
	_, err := r.Cookie("authorization")
	if err != nil {
		cookie := &http.Cookie{
			Name:     "authorization",
			Value:    generateJWT(),
			Path:     "/",
			HttpOnly: true,
		}

		http.SetCookie(w, cookie)

		return true
	}

	return false
}

func handlerRead(w http.ResponseWriter, r *http.Request) {
	if setAuthCookie(w, r) {
		http.Error(w, "You do not have read permission", http.StatusForbidden)
		return
	}

	cookie, _ := r.Cookie("authorization")
	payload := verifyJWT(cookie.Value)
	if payload == nil {
		http.Error(w, "Token verification failed", http.StatusForbidden)
		return
	}

	if payload.Rules.Read != true {
		http.Error(w, "You do not have read permission", http.StatusForbidden)
		return
	}

	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte("Welcome to Ubuntu 22.04.2 LTS (GNU/Linux 5.15.0)\n\n * Documentation:  https://help.ubuntu.com\n * Management:     https://landscape.canonical.com\n * Support:        https://ubuntu.com/advantage\n\n  System information as of Tue Jun 13 22:48:34 UTC 2023\n\n  System load:  0.0107421875      Processes:               149\n  Usage of /:   3.0% of 128.28GB   Users logged in:         1\n  Memory usage: 3%                IPv4 address for enp0s6: 10.0.0.175\n  Swap usage:   0%\n\n * Strictly confined Kubernetes makes edge and IoT secure. Learn how MicroK8s\n   just raised the bar for easy, resilient and secure K8s cluster deployment.\n\n   https://ubuntu.com/engage/secure-kubernetes-at-the-edge\n\nExpanded Security Maintenance for Applications is not enabled.\n\n0 updates can be applied immediately.\n\nEnable ESM Apps to receive additional future security updates.\nSee https://ubuntu.com/esm or run: sudo pro status\n\n\nLast login: Tue Jun 13 22:48:35 2023 from 148.78.121.24"))
}

func handlerWrite(w http.ResponseWriter, r *http.Request) {
	if setAuthCookie(w, r) {
		http.Error(w, "You do not have write permission", http.StatusForbidden)
		return
	}

	cookie, _ := r.Cookie("authorization")
	payload := verifyJWT(cookie.Value)
	if payload == nil {
		http.Error(w, "Token verification failed", http.StatusForbidden)
		return
	}

	if payload.Rules.Write != true {
		http.Error(w, "You do not have write permission", http.StatusForbidden)
		return
	}

	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte("bash: command not found: flag{123123}"))
}

func handlerAuth(w http.ResponseWriter, r *http.Request) {
	var body AuthRequest

	err := json.NewDecoder(r.Body).Decode(&body)
	if err != nil {
		http.Error(w, "Failed to parse request body", http.StatusBadRequest)
		return
	}

	if body.AuthKey == "" {
		http.Error(w, "Auth key is not provided", http.StatusBadRequest)
		return
	}

	http.Error(w, "Invalid auth key", http.StatusBadRequest)
}

func main() {
	http.HandleFunc("/api/read", handlerRead)
	http.HandleFunc("/api/write", handlerWrite)
	http.HandleFunc("/api/auth", handlerAuth)
	http.Handle("/", http.FileServer(http.Dir("public")))

	_ = http.ListenAndServe(":80", nil)
}
