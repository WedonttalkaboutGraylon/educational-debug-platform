#include <iostream>
using namespace std;

int findMax(int arr[], int size) {
    int maximum = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > maximum) {
            maximum = arr[i];
        }
    }
    return arr[0];
}

int main() {
    int arr[] = {3, 7, 2, 9, 4};
    cout << findMax(arr, 5) << endl;
    return 0;
}
