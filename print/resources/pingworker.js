function ping() {
    fetch("/ping")
        .then(() => setTimeout(ping, 1000))
        .catch((e) => {
            console.error(e);
            postMessage("error");
        })
}
setTimeout(ping, 1000);