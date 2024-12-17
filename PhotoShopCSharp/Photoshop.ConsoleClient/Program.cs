using System.Drawing;
using Photoshop.ConsoleClient.Implementation;

namespace Photoshop.ConsoleClient
{
    internal class Program
    {
        private const double GAMMA_VALUE = 2.6;  // Darker: >1, Brighter: <1, No change: =1
        private const double C = 10;  // 0~255
        private const int KERNEL_SIZE = 3;  // 3, 4, 5

        static void Main(string[] args)
        {
            string image_name = "oe.jpg";
            Bitmap input_image = ReadImage(image_name);
            // Negate
            Run(image_name, input_image, () => new Negate());
            // Gamma Transformation
            Run(image_name, input_image, () => new GammaTransformation(GAMMA_VALUE));
            // Logarithmic Transformation
            Run(image_name, input_image, () => new LogarithmicTransformation(C));
            // GrayScale
            Run(image_name, input_image, () => new GrayScale());
            // Mean Filter
            Run(image_name, input_image, () => new MeanFilter(KERNEL_SIZE));
        }

        private static Bitmap ReadImage(string image_name)
        {
            string input_image_path = Path.Combine(AppContext.BaseDirectory, "Resources", "Input", image_name);
            Bitmap result = input_image_path != null
                ? new Bitmap(input_image_path)
                : throw new ArgumentException($"Error reading {image_name}");
            return result;
        }

        private static void Run<T>(string image_name, Bitmap image, Func<T> factory) where T : _ImageProcessor
        {
            T processor = factory();
            Bitmap output_image = processor.Process(image);
            
            string output_image_path = Path.Combine(AppContext.BaseDirectory, "Resources", "Output", processor.GetType().Name + "_" + image_name);

            string output_directory = Path.GetDirectoryName(output_image_path);
            if (!Directory.Exists(output_directory))
            {
                Directory.CreateDirectory(output_directory);
            }
            output_image.Save(output_image_path);

            Console.WriteLine($"Image processed with {processor.GetType().Name}");
        }
    }
}