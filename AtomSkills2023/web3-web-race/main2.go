package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
)

func main() {
	var wg sync.WaitGroup
	wg.Add(1000)

	for i := 0; i < 1000; i++ {
		go func() {
			defer wg.Done()

			payload := map[string]interface{}{
				"username": "user2",
				"amount":   100,
			}

			jsonPayload, err := json.Marshal(payload)
			if err != nil {
				fmt.Printf("Ошибка при сериализации JSON: %s\n", err)
				return
			}

			// Создаем запрос
			req, err := http.NewRequest("POST", "http://127.0.0.1/api/send", bytes.NewBuffer(jsonPayload))
			if err != nil {
				fmt.Printf("Ошибка при создании запроса: %s\n", err)
				return
			}

			// Устанавливаем заголовок Cookie
			cookie := &http.Cookie{
				Name:  "authorization",
				Value: "84f2eda7-41e8-4898-b56d-242b98f5d78a",
			}

			req.AddCookie(cookie)

			// Отправляем запрос
			client := &http.Client{}
			resp, err := client.Do(req)
			if err != nil {
				fmt.Printf("Ошибка при выполнении запроса: %s\n", err)
				return
			}
			defer resp.Body.Close()

			fmt.Printf("Статус код для: %d\n", resp.StatusCode)
		}()
	}

	wg.Wait()
}
