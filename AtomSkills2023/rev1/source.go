package main

import (
	"fmt"
	"encoding/hex"
)

var key = "GOlan"
var test1 = "3327093e0c743c183e2928"
var test2 = "0b2e02063135743933175f"

func main() {

	fmt.Println("Введите флаг:")
	var flag string
	fmt.Scanln(&flag)

	flag1 := flag[:len(flag)/2]
	flag2 := flag[len(flag)/2:]

	enc1 := enc(flag1, key)
	enc2 := enc(flag2, SecondKey())
	
	if hex.EncodeToString([]byte(enc1+enc2)) != test1 + test2 {
		fmt.Println("Try Harder")
	} else {
		fmt.Println("Yeaap, that was flag.")
	}

}

func enc(s, key string) string {
	result := ""
	for i := 0; i < len(s); i++ {
		result += string(s[i] ^ key[i%len(key)])
	}
	return result
}

func SecondKey() string {
	second := key + string(key[0])
	return string(second)
}