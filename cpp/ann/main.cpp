#include <iostream>
#include <tuple>

#include "image.hpp"

using namespace std;
using mybits::Image;
using mybits::Color;

constexpr const char* path = "/home/d4de/Pictures/desktop.png";

int
main()
{
    size_t width, height;
    Image<mybits::ImagePNG> img(path);

    tie(width, height) = img.get_size();
    auto pixels = img.get_pixels();

    cout << "width: " << width << endl;
    cout << "height: " << height << endl;
    cout << "num of pixels: " << pixels.size() << endl;
    return 0;
}
