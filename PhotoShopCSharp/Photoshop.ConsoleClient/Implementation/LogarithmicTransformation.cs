using System.Drawing;

namespace Photoshop.ConsoleClient.Implementation
{
    public class LogarithmicTransformation(double c = 255) : _ImageProcessor
    {
        private readonly double _c = c;

        private protected override Bitmap Apply(Bitmap image)
        {
            Bitmap transformed_image = new(image.Width, image.Height);

            for (int y = 0; y < image.Height; y++)
            {
                for (int x = 0; x < image.Width; x++)
                {
                    Color original_color = image.GetPixel(x, y);

                    int r = (int)(this._c * Math.Log(1 + original_color.R));
                    int g = (int)(this._c * Math.Log(1 + original_color.G));
                    int b = (int)(this._c * Math.Log(1 + original_color.B));

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
