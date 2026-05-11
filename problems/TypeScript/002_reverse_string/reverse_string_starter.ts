function reverseString(str: string): string {
    let reversed = "";
    for (let i = str.length - 2; i >= 0; i--) {
        reversed += str[i];
    }
    return reversed;
}
