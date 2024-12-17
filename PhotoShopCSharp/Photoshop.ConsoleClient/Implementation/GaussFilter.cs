using System.Drawing;

namespace Photoshop.ConsoleClient.Implementation
{
    public class GaussFilter(int kernel_size = 3, double sigma = 1.0) : _ImageProcessor
    {
        private readonly int _kernel_size = (kernel_size % 2 == 1) ? kernel_size : kernel_size + 1;  // If not an odd number make it so
        private readonly double _sigma = sigma;

        private double[,] GenerateKernel()
        {
            int offset = this._kernel_size / 2;
            double[,] kernel = new double[this._kernel_size, this._kernel_size];
            double sum = 0.0;

            for (int y = -offset; y <= offset; y++)
            {
                for (int x = -offset; x <= offset; x++)
                {
                    double value = Math.Exp(-(x * x + y * y) / (2 * this._sigma * this._sigma)) / (2 * Math.PI * this._sigma * this._sigma);
                    kernel[y + offset, x + offset] = value;
                    sum += value;
                }
            }
            // Normalize Kernel
            for (int y = 0; y < this._kernel_size; y++)
            {
                for(int x = 0; x < this._kernel_size; x++)
                {
                    kernel[y, x] /= sum;
                }
            }

            return kernel;
        }

        private protected override Bitmap Apply(Bitmap image)
        {
            int width = image.Width;
            int height = image.Height;
            Bitmap filtered_image = new(width, height);

            double[,] kernel = GenerateKernel();
            int offset = this._kernel_size / 2;

            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    double sum_r = 0, sum_g = 0, sum_b = 0;

                    for (int ky = -offset; ky <= offset; ky++)
                    {
                        for (int kx = -offset; kx <= offset; kx++)
                        {
                            int pixel_x = x + kx;
                            int pixel_y = y + ky;

                            if ((pixel_x >= 0) && (pixel_x < width) && (pixel_y >= 0) && (pixel_y < height))
                            {
                                Color neighbor_color = image.GetPixel(pixel_x, pixel_y);
                                double weight = kernel[ky + offset, kx + offset];

                                sum_r += neighbor_color.R * weight;
                                sum_g += neighbor_color.G * weight;
                                sum_b += neighbor_color.B * weight;
                            }
                        }
                    }
                    int new_r = Math.Min(255, Math.Max(0, (int)sum_r));
                    int new_g = Math.Min(255, Math.Max(0, (int)sum_g));
                    int new_b = Math.Min(255, Math.Max(0, (int)sum_b));

                    filtered_image.SetPixel(x, y, Color.FromArgb(new_r, new_g, new_b));
                }
            }
            return filtered_image;
        }
    }
}
