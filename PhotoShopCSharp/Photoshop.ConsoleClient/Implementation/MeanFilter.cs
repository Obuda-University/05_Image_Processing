using System.Drawing;

namespace Photoshop.ConsoleClient.Implementation
{
    public class MeanFilter(int kernel_size = 3) : _ImageProcessor
    {
        private readonly int _kernel_size = kernel_size;

        private protected override Bitmap Apply(Bitmap image)
        {
            int width = image.Width;
            int height = image.Height;
            Bitmap filtered_image = new(width, height);
            int offset = this._kernel_size / 2;

            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    int sum_r = 0, sum_g = 0, sum_b = 0;
                    int count = 0;

                    for (int ky = -offset; ky <= offset; ky++)
                    {
                        for (int kx = -offset; kx <= offset; kx++)
                        {
                            int pixel_x = x + kx;
                            int pixel_y = y + ky;

                            if ((pixel_x >= 0) && (pixel_x < width) && (pixel_y >= 0) && (pixel_y < height))
                            {
                                Color neighbor_color = image.GetPixel(pixel_x, pixel_y);
                                sum_r += neighbor_color.R;
                                sum_g += neighbor_color.G;
                                sum_b += neighbor_color.B;
                                count++;
                            }
                        }
                    }

                    int avg_r = sum_r / count;
                    int avg_g = sum_g / count;
                    int avg_b = sum_b / count;

                    filtered_image.SetPixel(x, y, Color.FromArgb(avg_r, avg_g, avg_b));
                }
            }
            return filtered_image;
        }
    }
}
