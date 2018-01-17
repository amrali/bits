#ifndef MYBITS_IMAGE_HPP
#define MYBITS_IMAGE_HPP

#include <string>
#include <memory>
#include <tuple>
#include <vector>

#include <stdio.h>
#include <gd.h>

namespace mybits
{

    constexpr int ImagePNG = 1;

    typedef gdImagePtr image_pointer;

    struct Color
    {
        typedef std::tuple<int, int, int, int> color_type;

        Color() = default;
        Color(image_pointer, int);
        Color(int, int, int, int);

        operator int() const;
        operator const color_type&() const;

    private:
        color_type _M_color;
    };

    template <int Type>
    struct Image
    {
        typedef std::shared_ptr<gdImage> image_type;
        typedef std::tuple<size_t, size_t> size_type;
        typedef std::vector<Color> pixels_array_type;

        Image() = default;
        Image(const std::string&);

        operator image_pointer() const;

        Color get_pixel(int x, int y) const;
        size_type get_size() const;
        pixels_array_type get_pixels() const;

    private:
        typedef std::shared_ptr<FILE> FDPtr;
        FDPtr _Mp_fd;
        image_type _Mp_img;
    };

} // namespace mybits

#endif // MYBITS_IMAGE_HPP
