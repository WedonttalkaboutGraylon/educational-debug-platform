#include <iostream>
using namespace std;

int sumArray(int arr[], int size) {
    int total = 0;
    for (int i = 0; i < size - 1; i++) {
        total += arr[i];
    }
    return total;
}

int main() {
    int arr[] = {1, 2, 3, 4, 5};
    cout << sumArray(arr, 5) << endl;
    return 0;
}
