#include <tuple>
#include <stdexcept>
#include <cstring>
#include <cerrno>
#include <stdio.h>

#include "image.hpp"

namespace mybits
{

    // Color

    Color::Color(int red, int green, int blue, int alpha) :
        _M_color(red, green, blue, alpha)
    {}

    Color::Color(image_pointer img, int color) :
        Color(
                gdImageRed(img, color),
                gdImageGreen(img, color),
                gdImageBlue(img, color),
                gdImageAlpha(img, color)
                )
    {}

    Color::operator int() const
    {
        int red, green, blue, alpha;
        std::tie(red, green, blue, alpha) = _M_color;
        return gdTrueColorAlpha(red, green, blue, alpha);
    }

    Color::operator const Color::color_type&() const
    {
        return _M_color;
    }

    // Image

    template <int Type>
    Image<Type>::Image(const std::string& filename)
    {
        _Mp_fd = FDPtr(fopen(filename.c_str(), "r+bm"), fclose);
        if(!_Mp_fd)
            throw std::runtime_error(strerror(errno));

        switch (Type)
        {
            case ImagePNG:
                _Mp_img = image_type(gdImageCreateFromPng(_Mp_fd.get()),
                        gdImageDestroy);
                break;
            default:
                throw std::runtime_error("template parameter Type is invalid");
        }
    }

    template <int Type>
    Image<Type>::operator image_pointer() const
    {
        return _Mp_img.get();
    }

    template <int Type>
    Color
    Image<Type>::get_pixel(int x, int y) const
    {
        int color;
        switch (Type)
        {
            case ImagePNG:
                color = gdImageGetTrueColorPixel(_Mp_img.get(), x, y);
                return Color(*this, color);
            default:
                throw std::runtime_error("template parameter Type is invalid");
        }
    }

    template <int Type>
    typename Image<Type>::size_type
    Image<Type>::get_size() const
    {
        return size_type(gdImageSX(_Mp_img.get()), gdImageSY(_Mp_img.get()));
    }

    template <int Type>
    typename Image<Type>::pixels_array_type
    Image<Type>::get_pixels() const
    {
        size_t width, height;

        std::tie(width, height) = get_size();
        pixels_array_type result;

        result.reserve(width * height);
        for (size_t y = 0; y < height; ++y)
        {
            for (size_t x = 0; x < width; ++x)
            {
                result.push_back(get_pixel(x, y));
            }
        }

        return result;
    }

    template struct Image<ImagePNG>;

} // namespace mybits
