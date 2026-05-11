function removeDuplicates(numbers: number[]): number[] {
    const seen = new Set<number>();
    const result: number[] = [];
    for (const num of numbers) {
        if (!seen.has(num)) {
            seen.add(num);
            result.push(num);
        }
    }
    return numbers;
}
