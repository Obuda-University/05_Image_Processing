using System.Drawing;

namespace Photoshop.ConsoleClient
{
    public class Negate : ImageProcessor
    {
        private protected override Bitmap Apply(Bitmap image)
        {
            Bitmap negated_image = new(image.Width, image.Height);

            for (int y = 0; y < image.Height; y++)
            {
                for (int x = 0; x < image.Width; x++)
                {
                    Color original_color = image.GetPixel(x, y);

                    Color negated_color = Color.FromArgb(
                            original_color.A,
                            255 - original_color.R,
                            255 - original_color.G,
                            255 - original_color.B
                    );

                    negated_image.SetPixel(x, y, negated_color);
                }
            }

            return negated_image;
        }
    }
}
