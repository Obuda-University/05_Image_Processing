using System.Drawing;

namespace Photoshop.ConsoleClient
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string image_name = "oe.jpg";
            Bitmap input_image = ReadImage(image_name);

            Run(image_name, input_image, () => new Negate());
        }

        private static Bitmap ReadImage(string image_name)
        {
            string input_image_path = Path.Combine(AppContext.BaseDirectory, "Resources", "Input", image_name);
            Bitmap result = input_image_path != null
                ? new Bitmap(input_image_path)
                : throw new ArgumentException($"Error reading {image_name}");
            return result;
        }

        private static void Run<T>(string image_name, Bitmap image, Func<T> factory) where T : ImageProcessor
        {
            T processor = factory();

            Bitmap output_image = processor.Process(image);
            string output_image_path = Path.Combine(AppContext.BaseDirectory, "Resources", "Output", image_name);

            string output_directory = Path.GetDirectoryName(output_image_path);
            if (!Directory.Exists(output_directory))
            {
                Directory.CreateDirectory(output_directory);
            }
            output_image.Save(output_image_path);

            Console.WriteLine($"Image processed with {processor.GetType().Name} and saved to: {output_image_path}");
        }
    }
}