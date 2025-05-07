using WebPage.Models;

namespace WebPage.Repositry.IRepositry
{
    public interface ISearchService
    {
        Task<IEnumerable<SearchResult>> SearchAsync(string word);
    }
}
