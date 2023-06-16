package main

import (
	"encoding/json"
	"fmt"
	"github.com/google/uuid"
	"net/http"
	"strconv"
	"sync"
	"time"
)

type AuthRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type PromoRequest struct {
	Code string `json:"code"`
}

type BuyRequest struct {
	Position int `json:"position"`
}

type SendRequest struct {
	Username string `json:"username"`
	Amount   int    `json:"amount"`
}

type User struct {
	Username string
	Password string
	Promo    bool
	Session  string
	Amount   int
}

func handlerPromo(users []User) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		cookie, err := r.Cookie("authorization")
		if err != nil {
			http.Error(w, "Session not found", http.StatusBadRequest)
			return
		}

		var user *User

		for i := range users {
			if users[i].Session == cookie.Value {
				user = &users[i]
				break
			}
		}

		if user == nil {
			http.Error(w, "Session not found", http.StatusBadRequest)
			return
		}

		var body PromoRequest

		err = json.NewDecoder(r.Body).Decode(&body)
		if err != nil {
			http.Error(w, "Failed to parse request body", http.StatusBadRequest)
			return
		}

		if body.Code != "ONEHUNDRED" {
			http.Error(w, "Code not found", http.StatusBadRequest)
			return
		}

		if user.Promo == true {
			http.Error(w, "You have already used this code", http.StatusBadRequest)
			return
		}

		user.Promo = true
		user.Amount += 100

		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(strconv.Itoa(user.Amount)))
	}
}

func handlerBuy(users []User) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		cookie, err := r.Cookie("authorization")
		if err != nil {
			http.Error(w, "Session not found", http.StatusBadRequest)
			return
		}

		var user *User

		for i := range users {
			if users[i].Session == cookie.Value {
				user = &users[i]
				break
			}
		}

		if user == nil {
			http.Error(w, "Session not found", http.StatusBadRequest)
			return
		}

		var body BuyRequest

		err = json.NewDecoder(r.Body).Decode(&body)
		if err != nil {
			http.Error(w, "Failed to parse request body", http.StatusBadRequest)
			return
		}

		if body.Position != 1 && body.Position != 2 && body.Position != 3 {
			http.Error(w, "Position not found", http.StatusBadRequest)
			return
		}

		if user.Amount < 300 {
			http.Error(w, "You need 300 coins", http.StatusBadRequest)
			return
		}

		user.Amount -= 300

		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(fmt.Sprintf("%s.%s", strconv.Itoa(user.Amount), "flag{123123}")))
	}
}

func handlerOpen(users []User) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		cookie, err := r.Cookie("authorization")
		if err != nil {
			w.WriteHeader(http.StatusNoContent)
			return
		}

		var user *User

		for i := range users {
			if users[i].Session == cookie.Value {
				user = &users[i]
				break
			}
		}

		if user == nil {
			w.WriteHeader(http.StatusNoContent)
			return
		}

		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(strconv.Itoa(user.Amount)))
	}
}

func handlerAuth(users []User) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var body AuthRequest

		err := json.NewDecoder(r.Body).Decode(&body)
		if err != nil {
			http.Error(w, "Failed to parse request body", http.StatusBadRequest)
			return
		}

		if body.Username == "" {
			http.Error(w, "Username is not provided", http.StatusBadRequest)
			return
		}

		if body.Password == "" {
			http.Error(w, "Password is not provided", http.StatusBadRequest)
			return
		}

		var user *User

		for i := range users {
			if users[i].Username == body.Username && users[i].Password == body.Password {
				user = &users[i]
				break
			}
		}

		if user == nil {
			http.Error(w, "Username or password entered incorrectly", http.StatusBadRequest)
			return
		}

		cookie := &http.Cookie{
			Name:     "authorization",
			Value:    uuid.New().String(),
			Path:     "/",
			HttpOnly: true,
		}

		user.Session = cookie.Value
		http.SetCookie(w, cookie)

		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(strconv.Itoa(user.Amount)))
	}
}

type ThrottlerRequest struct {
	Writer  http.ResponseWriter
	Request *http.Request
	Users   []User
	Done    chan struct{}
}

type Throttler struct {
	Mut      sync.Mutex
	Users    []User
	Requests []*ThrottlerRequest
}

var mutex sync.Mutex

func (tr *ThrottlerRequest) Handler() {
	cookie, err := tr.Request.Cookie("authorization")
	if err != nil {
		http.Error(tr.Writer, "Session not found", http.StatusBadRequest)
		return
	}

	var user *User

	for i := range tr.Users {
		if tr.Users[i].Session == cookie.Value {
			user = &tr.Users[i]
			break
		}
	}

	if user == nil {
		http.Error(tr.Writer, "Session not found", http.StatusBadRequest)
		return
	}

	var body SendRequest

	err = json.NewDecoder(tr.Request.Body).Decode(&body)
	if err != nil {
		http.Error(tr.Writer, "Failed to parse request body", http.StatusBadRequest)
		return
	}

	if body.Amount <= 0 {
		http.Error(tr.Writer, "The amount must be greater than or equal to 1", http.StatusBadRequest)
		return
	}

	if body.Amount > user.Amount {
		http.Error(tr.Writer, "You don't have that many coins", http.StatusBadRequest)
		return
	}

	var target *User

	for i := range tr.Users {
		if tr.Users[i].Username == body.Username {
			target = &tr.Users[i]
			break
		}
	}

	if target == nil {
		http.Error(tr.Writer, "Coin transfer client not found", http.StatusBadRequest)
		return
	}

	mutex.Lock()
	user.Amount -= body.Amount
	target.Amount += body.Amount
	fmt.Println(user, target)
	mutex.Unlock()

	tr.Writer.WriteHeader(http.StatusOK)
	_, _ = tr.Writer.Write([]byte(strconv.Itoa(user.Amount)))
}

func (t *Throttler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	done := make(chan struct{})

	t.Mut.Lock()
	t.Requests = append(t.Requests, &ThrottlerRequest{Writer: w, Request: r, Users: t.Users, Done: done})
	count := len(t.Requests)
	t.Mut.Unlock()

	if count == 1 {
		go func() {
			time.Sleep(time.Millisecond * 20)
			t.Mut.Lock()
			requests := t.Requests
			t.Requests = nil
			t.Mut.Unlock()

			for _, request := range requests {
				go func(tr *ThrottlerRequest) {
					tr.Handler()
					close(tr.Done)
				}(request)
			}
		}()
	}

	<-done
}

func main() {
	users := []User{
		{
			Username: "dunushkin-pv",
			Password: "OHwQT1if",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "sedykh-dv",
			Password: "kvZmVY17",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "prostitov-av",
			Password: "eAXl2uG0",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "romanchenko-sn",
			Password: "eG8V3C6q",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "zenkova-es",
			Password: "60zUntFm",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "skorobogatova-n",
			Password: "Zi5ivDEi",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "neveykin-og",
			Password: "fgJywm4j",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "semenkin-kk",
			Password: "83eUNsTa",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "kirnas-vu",
			Password: "5ZBTjcro",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "kolmogorov-as",
			Password: "9JWS5zgr",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "belyaev-id",
			Password: "F4TDcmUe",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "malahov-ak",
			Password: "vTclLpD9",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "bogdanov-da",
			Password: "u8nMJHtL",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "morozov-aa",
			Password: "qeOAa81g",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "balobanov-ma",
			Password: "hMnG602o",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "konstantinova-ia",
			Password: "toV5mpBu",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "osipova-ps",
			Password: "RskFh1GQ",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "vyalikh-pv",
			Password: "ptH6s61s",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "kotov-ei",
			Password: "9XNDS8Us",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "korchagin-va",
			Password: "Mmv7oPrS",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "titov-ik",
			Password: "zYd10TkH",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "velikoivanenko-eo",
			Password: "YkmVB0ph",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "aldabergenov-n",
			Password: "9I0gotUd",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "rodionov-da",
			Password: "eJnyT6EQ",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "maksimova-ep",
			Password: "45JT0SDi",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "vlasov-dv",
			Password: "qOIx4YyS",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "dias",
			Password: "JA54dVvJ",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
		{
			Username: "yarchuk-dk",
			Password: "a3LBQ69K",
			Promo:    false,
			Session:  "",
			Amount:   0,
		},
	}

	http.HandleFunc("/api/auth", handlerAuth(users))
	http.HandleFunc("/api/open", handlerOpen(users))
	http.HandleFunc("/api/promo", handlerPromo(users))
	http.HandleFunc("/api/buy", handlerBuy(users))
	http.Handle("/api/send", &Throttler{Users: users})

	http.Handle("/", http.FileServer(http.Dir("svelte/build")))

	_ = http.ListenAndServe(":80", nil)
}
