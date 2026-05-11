#include <iostream>
using namespace std;

int countPositive(int arr[], int size) {
    int count = 0;
    for (int i = 0; i < size; i++) {
        if (arr[i] <= 0) {
            count++;
        }
    }
    return count;
}

int main() {
    int arr[] = {1, -2, 3, -4, 5};
    cout << countPositive(arr, 5) << endl;
    return 0;
}
