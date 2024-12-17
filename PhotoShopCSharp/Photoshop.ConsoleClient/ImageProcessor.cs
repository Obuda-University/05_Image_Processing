using System.Drawing;

namespace Photoshop.ConsoleClient
{
    public abstract class ImageProcessor
    {
        public Bitmap Process(Bitmap image)
        {
            return image == null ? throw new ArgumentNullException(nameof(image)) : Apply(image);
        }

        private protected abstract Bitmap Apply(Bitmap bitmap);
    }
}
