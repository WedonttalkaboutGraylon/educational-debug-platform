function countVowels(str: string): number {
    const vowels = "aeiou";
    let count = 0;
    for (const char of str) {
        if (vowels.includes(char)) {
            count++;
        }
    }
    return count;
}
