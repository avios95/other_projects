#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
using namespace std;


int main() {
    ifstream f("settings.conf");
    string str;
    string delimiter = "Greeting = ";
    size_t pos = 0;
    string token;

    if(f) {
        ostringstream ss;
        ss << f.rdbuf();
        str = ss.str();

        while ((pos = str.find(delimiter)) != string::npos) {
            token = str.substr(0, pos);
            str.erase(0, pos + delimiter.length());
        }
    }

    cout << str;
}
