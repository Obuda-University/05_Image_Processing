using System.Drawing;

namespace Photoshop.ConsoleClient.Implementation
{
    public class GrayScale : _ImageProcessor
    {
        private protected override Bitmap Apply(Bitmap image)
        {
            Bitmap grayscaled_image = new(image.Width, image.Height);

            for (int y = 0; y < image.Height; y++)
            {
                for (int x = 0; x < image.Width; x++)
                {
                    Color original_color = image.GetPixel(x, y);
                    int gray_intensity = (int)(0.299 * original_color.R + 0.587 * original_color.G + 0.114 * original_color.B);
                    // 0~255
                    gray_intensity = Math.Min(255, Math.Max(0, gray_intensity));

                    grayscaled_image.SetPixel(x, y, Color.FromArgb(original_color.A, gray_intensity, gray_intensity, gray_intensity));
                }
            }
            return grayscaled_image;
        }
    }
}
