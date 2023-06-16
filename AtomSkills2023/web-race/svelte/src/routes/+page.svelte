<script>
    import {Button} from "$components/ui/button"
    import {Card, CardContent, CardFooter, CardHeader, CardTitle} from "$components/ui/card"
    import {Label} from "$components/ui/label"
    import {Input} from "$components/ui/input"
    import {onMount} from "svelte";

    let amount = -1

    onMount(() => fetch("/api/open")
        .then((r) => r.text()).then((d) => {if (d) amount = Number(d)}))

    let auth_open = false
    let auth_username = ""
    let auth_password = ""
    let auth_error = ""

    const auth = () => {
        fetch("/api/auth", {
            method: "POST",
            body: JSON.stringify({username: auth_username, password: auth_password})
        })
            .then((response) => response.text()
                .then((data) => ({status: response.status, data: data})))
            .then((response) => {
                if (response.status !== 200) {
                    auth_error = response.data
                } else {
                    auth_username = ""
                    auth_password = ""
                    auth_error = ""
                    auth_open = false
                    amount = Number(response.data)
                }
            })
    }

    let promo_open = false
    let promo_input = ""
    let promo_error = ""

    const promo = () => {
        fetch("/api/promo", {
            method: "POST",
            body: JSON.stringify({code: promo_input})
        })
            .then((response) => response.text()
                .then((data) => ({status: response.status, data: data})))
            .then((response) => {
                if (response.status !== 200) {
                    promo_error = response.data
                } else {
                    promo_input = ""
                    promo_error = ""
                    promo_open = false
                    amount = Number(response.data)
                }
            })
    }

    let buy_pos = -1
    let buy_code = ""
    let buy_error = ""

    let buy_timeout
    const buy = () => {
        clearTimeout(buy_timeout)

        fetch("/api/buy", {
            method: "POST",
            body: JSON.stringify({position: buy_pos})
        })
            .then((response) => response.text()
                .then((data) => ({status: response.status, data: data})))
            .then((response) => {
                if (response.status !== 200) {
                    buy_error = response.data
                } else {
                    const split = response.data.split(".")

                    buy_error = ""
                    buy_code = split[1]
                    amount = Number(split[0])
                }
            })

        buy_timeout = setTimeout(() => {
            if (!buy_code) {
                buy_error = ""
                buy_pos = -1
            }
        }, 5000)
    }

    let send_open = false
    let send_username = ""
    let send_amount = ""
    let send_error = ""

    const send = () => {
        fetch("/api/send", {
            method: "POST",
            body: JSON.stringify({username: send_username, amount: Number(send_amount)})
        })
            .then((response) => response.text()
                .then((data) => ({status: response.status, data: data})))
            .then((response) => {
                if (response.status !== 200) {
                    send_error = response.data
                } else {
                    send_open = false
                    send_username = ""
                    send_amount = ""
                    send_error = ""
                    amount = Number(response.data)
                }
            })
    }
</script>

{#if (auth_open)}
    <div class="absolute top-0 left-0 right-0 bottom-0 z-10 bg-black/50 flex items-center justify-center"
         on:click={() => auth_open = false}>
        <Card class="w-4/12 p-8 pt-6 flex flex-col gap-4" on:click={(event) => event.stopPropagation()}>
            <CardHeader class="space-y-1">
                <CardTitle class="text-2xl text-center">Авторизация</CardTitle>
            </CardHeader>
            <CardContent class="grid gap-6">
                <div class="grid gap-2">
                    <Label for="username">Имя пользователя</Label>
                    <Input id="username" bind:value={auth_username}/>
                </div>
                <div class="grid gap-2">
                    <Label for="password">Пароль</Label>
                    <Input id="password" type="password" bind:value={auth_password}/>
                </div>
                {#if (auth_error)}<span class="text-sm text-red-500">Ошибка: {auth_error}</span>{/if}
            </CardContent>
            <CardFooter>
                <Button class="w-full" on:click={() => auth()}>Войти</Button>
            </CardFooter>
        </Card>
    </div>
{/if}

{#if (promo_open)}
    <div class="absolute top-0 left-0 right-0 bottom-0 z-10 bg-black/50 flex items-center justify-center"
         on:click={() => promo_open = false}>
        <Card class="w-4/12 p-8 pt-6 flex flex-col gap-4" on:click={(event) => event.stopPropagation()}>
            <CardHeader class="space-y-1">
                <CardTitle class="text-2xl text-center">Активировать промо-код</CardTitle>
            </CardHeader>
            <CardContent class="grid gap-6">
                <div class="grid gap-2">
                    <Label for="promo">Промо-код</Label>
                    <Input id="promo" bind:value={promo_input}/>
                </div>
                {#if (promo_error)}<span class="text-sm text-red-500">Ошибка: {promo_error}</span>{/if}
            </CardContent>
            <CardFooter>
                <Button class="w-full" on:click={() => promo()}>Продолжить</Button>
            </CardFooter>
        </Card>
    </div>
{/if}

{#if (send_open)}
    <div class="absolute top-0 left-0 right-0 bottom-0 z-10 bg-black/50 flex items-center justify-center"
         on:click={() => send_open = false}>
        <Card class="w-4/12 p-8 pt-6 flex flex-col gap-4" on:click={(event) => event.stopPropagation()}>
            <CardHeader class="space-y-1">
                <CardTitle class="text-2xl text-center">Перевести монеты клиенту</CardTitle>
            </CardHeader>
            <CardContent class="grid gap-6">
                <div class="grid gap-2">
                    <Label for="target">Имя пользователя (Получателя)</Label>
                    <Input id="target" bind:value={send_username}/>
                </div>
                <div class="grid gap-2">
                    <Label for="amount">Количество монет</Label>
                    <Input id="amount" bind:value={send_amount}/>
                </div>
                {#if (send_error)}<span class="text-sm text-red-500">Ошибка: {send_error}</span>{/if}
            </CardContent>
            <CardFooter>
                <Button class="w-full" on:click={() => send()}>Отправить</Button>
            </CardFooter>
        </Card>
    </div>
{/if}

<div class="h-screen flex flex-col">
    <div class="border-b p-8 pt-6 flex items-center justify-between">
        <h2 class="text-3xl font-bold tracking-tight">Магазин NFT</h2>
        <div class="flex gap-4 items-center">
            {#if (amount === -1)}
                <span class="text-sm text-gray-500">Вы не авторизованы</span>
            {:else}
                <Button size="sm" class="bg-emerald-500 hover:bg-emerald-600" on:click={() => send_open = true}>
                    Перевести монеты
                </Button>
                <span class="text-sm text-gray-500">У вас {amount} монет</span>
            {/if}
        </div>
    </div>
    <div class="p-8 pt-6 h-full flex flex-col">
        <Card>
            <CardHeader class="pb-2">
                <CardTitle class="text-2xl font-bold">
                    Промо-код "<span class="text-red-500">O</span><span class="text-orange-500">N</span><span
                        class="text-yellow-500">E</span><span class="text-green-500">H</span><span class="text-sky-500">U</span><span
                        class="text-blue-500">N</span><span class="text-purple-500">D</span><span
                        class="text-red-500">R</span><span class="text-orange-500">E</span><span
                        class="text-yellow-500">D</span>"
                </CardTitle>
            </CardHeader>
            <CardContent class="flex items-center justify-between">
                <span class="text-1xl font-bold">Воспользуйся данным промо-кодом и получи <span
                        class="text-emerald-500">100 монет</span> совершенно бесплатно!</span>
                {#if (amount === -1)}
                    <Button size="sm" class="bg-emerald-500 hover:bg-emerald-600" on:click={() => auth_open = true}>
                        Авторизоваться
                    </Button>
                {:else}
                    <Button size="sm" class="bg-emerald-500 hover:bg-emerald-600" on:click={() => promo_open = true}>
                        Ввести промо-код
                    </Button>
                {/if}
            </CardContent>
        </Card>
        <div class="pt-12 flex gap-12 justify-between h-full">
            <Card class="w-full h-full flex flex-col">
                <CardHeader>
                    <img class="rounded-md" src="https://http.cat/images/102.jpg"/>
                </CardHeader>
                <CardContent class="h-full flex flex-col justify-between">
                    <div>
                        <CardTitle class="text-xl font-bold">#1 - Processing</CardTitle>
                        <span>Знаешь, почему безопасники боятся 102 кода ошибки? Потому что они думают, что сервер просто слишком долго думает, а на самом деле он просто смотрит на них с недоумением и пытается понять, как бы не помереть!</span>
                    </div>
                    {#if (buy_error && buy_pos === 1)}<span
                            class="text-sm text-red-500 text-center h-9 flex items-center justify-center">Ошибка: {buy_error}</span>{/if}
                    {#if (buy_code && buy_pos === 1)}<span
                            class="text-sm text-green-500 text-center h-9 flex items-center justify-center">Смарт-контракт: {buy_code}</span>{/if}
                    {#if (buy_pos !== 1)}
                        <Button size="sm" class="mt-4 bg-emerald-500 hover:bg-emerald-600"
                                on:click={() => {buy_pos = 1; buy()}} disabled={amount === -1 || buy_code}>Купить за 300
                            монет
                        </Button>
                    {/if}
                </CardContent>
            </Card>
            <Card class="w-full h-full flex flex-col">
                <CardHeader>
                    <img class="rounded-md" src="https://http.cat/images/418.jpg"/>
                </CardHeader>
                <CardContent class="h-full flex flex-col justify-between">
                    <div>
                        <CardTitle class="text-xl font-bold">#2 - I'm a teapot</CardTitle>
                        <span>Знаешь, почему безопасник выбрал 418 код ошибки? Потому что он решил, что самый безопасный способ защитить сервер - это превратить его в чайник и надеяться, что злоумышленники пойдут пить чай!</span>
                    </div>
                    {#if (buy_error && buy_pos === 2)}<span
                            class="text-sm text-red-500 text-center h-9 flex items-center justify-center">Ошибка: {buy_error}</span>{/if}
                    {#if (buy_code && buy_pos === 2)}<span
                            class="text-sm text-green-500 text-center h-9 flex items-center justify-center">Смарт-контракт: {buy_code}</span>{/if}
                    {#if (buy_pos !== 2)}
                        <Button size="sm" class="mt-4 bg-emerald-500 hover:bg-emerald-600"
                                on:click={() => {buy_pos = 2; buy()}} disabled={amount === -1 || buy_code}>Купить за 300
                            монет
                        </Button>
                    {/if}
                </CardContent>
            </Card>
            <Card class="w-full h-full flex flex-col">
                <CardHeader>
                    <img class="rounded-md" src="https://http.cat/images/508.jpg"/>
                </CardHeader>
                <CardContent class="h-full flex flex-col justify-between">
                    <div>
                        <CardTitle class="text-xl font-bold">#3 - Loop Detected</CardTitle>
                        <span>Тут должна быть самая смешная шутка, но ChatGPT начал так несмешно шутить, что прошлые 2 шутки еще даже ничего вроде...</span>
                    </div>
                    {#if (buy_error && buy_pos === 3)}<span
                            class="text-sm text-red-500 text-center h-9 flex items-center justify-center">Ошибка: {buy_error}</span>{/if}
                    {#if (buy_code && buy_pos === 3)}<span
                            class="text-sm text-green-500 h-9 flex items-center justify-center">Смарт-контракт: {buy_code}</span>{/if}
                    {#if (buy_pos !== 3)}
                        <Button size="sm" class="mt-4 bg-emerald-500 hover:bg-emerald-600"
                                on:click={() => {buy_pos = 3; buy()}} disabled={amount === -1 || buy_code}>Купить за 300
                            монет
                        </Button>
                    {/if}
                </CardContent>
            </Card>
        </div>
    </div>
</div>
