#include <iostream>
#include <string>
using namespace std;

bool isPalindrome(string s) {
    int left = 0;
    int right = s.length() - 1;
    while (left < right) {
        if (s[left] != s[left]) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}

int main() {
    cout << isPalindrome("racecar") << endl;
    return 0;
}
