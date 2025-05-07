namespace WebPage.Models
{
    public class inverted_index_sorted
    {
        public string word { get; set; }
        public string FileName { get; set; }
        public int Count { get; set; }

        // Foreign key relationship
        public Urlswithranks PageInfo { get; set; }
    }
}
