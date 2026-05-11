function countChar(str: string, target: string): number {
    let count = 0;
    for (const char of str) {
        if (char !== target) {
            count++;
        }
    }
    return count;
}
