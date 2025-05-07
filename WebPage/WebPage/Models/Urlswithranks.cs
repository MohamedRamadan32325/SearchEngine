namespace WebPage.Models
{
    public class Urlswithranks
    {
        public string URL { get; set; }
        public double PageRank { get; set; }
        public string FileName { get; set; }
        // Navigation property
        public ICollection<inverted_index_sorted> WordIndices { get; set; }
    }
}
