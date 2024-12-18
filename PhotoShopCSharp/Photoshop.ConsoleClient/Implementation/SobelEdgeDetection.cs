using System.Drawing;

namespace Photoshop.ConsoleClient.Implementation
{
    public class SobelEdgeDetection(Bitmap gray_image) : _ImageProcessor
    {
        private readonly Bitmap _gray_scaled_image = gray_image;

        private protected override Bitmap Apply(Bitmap image)
        {
            int width = image.Width;
            int height = image.Height;
            Bitmap sobel_image = new Bitmap(width, height);
            // Kernels
            int[,] sobel_x = new int[,] { { -1, 0, 1 }, { -2, 0, 2 }, { -1, 0, 1 } };
            int[,] sobel_y = new int[,] { { -1, -2, -1 }, { 0, 0, 0 }, { 1, 2, 1 } };

            for ( int x = 1; x < width - 1; x++ )
            {
                for ( int y = 1; y < height - 1; y++ )
                {
                    int pixel_x = 0, pixel_y = 0;

                    for (int kx = -1; kx <= 1; kx++)
                    {
                        for(int ky = -1; ky <= 1; ky++)
                        {
                            Color gray_color = this._gray_scaled_image.GetPixel(x + kx, y + ky);
                            int gray_value = gray_color.R;

                            pixel_x += gray_value * sobel_x[kx + 1, ky + 1];
                            pixel_y += gray_value * sobel_y[ky + 1, ky + 1];
                        }
                    }

                    int magnitude = (int)Math.Sqrt(pixel_x * pixel_x + pixel_y * pixel_y);
                    magnitude = Math.Min(255, magnitude);

                    sobel_image.SetPixel(x, y, Color.FromArgb(magnitude, magnitude, magnitude));
                }
            }
            return sobel_image;
        }
    }
}
