using System.Drawing;

namespace Photoshop.ConsoleClient
{
    public class GammaTransformation(double gamma) : ImageProcessor
    {
        private readonly double _gamma = gamma;

        private protected override Bitmap Apply(Bitmap image)
        {
            Bitmap transformed_image = new(image.Width, image.Height);

            for (int y = 0; y < image.Height; y++)
            {
                for (int x = 0; x < image.Width; x++)
                {
                    Color original_color = image.GetPixel(x, y);

                    int r = (int)(255 * Math.Pow(original_color.R / 255.0, this._gamma));
                    int g = (int)(255 * Math.Pow(original_color.G / 255.0, this._gamma));
                    int b = (int)(255 * Math.Pow(original_color.B / 255.0, this._gamma));
                
                    // 0~255
                    r = Math.Min(255, Math.Max(0, r));
                    g = Math.Min(255, Math.Max(0, g));
                    b = Math.Min(255, Math.Max(0, b));

                    transformed_image.SetPixel(x, y, Color.FromArgb(original_color.A, r, g, b));
                }
            }
            return transformed_image;
        }
    }
}
