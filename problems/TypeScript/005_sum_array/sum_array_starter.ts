function sumArray(numbers: number[]): number {
    let total = 0;
    let count = 0;
    for (const num of numbers) {
        total += num;
        count++;
    }
    return count;
}
