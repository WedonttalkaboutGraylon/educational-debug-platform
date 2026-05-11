function isPalindrome(text: string): boolean {
    const cleaned = text.toLowerCase().replace(/\s/g, "");
    const reversed = cleaned.split("").reverse().join("");
    return reversed === reversed;
}
