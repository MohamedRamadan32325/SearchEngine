using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WebPage.Data;
using WebPage.Models;
using WebPage.Repositry.IRepositry;

namespace WebPage.Repositry
{
    public class SearchService : ISearchService
    {
        private readonly AppDbContext _context;

        public SearchService(AppDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<SearchResult>> SearchAsync(string word)
        {
            // First, let's modify our models to include proper relationships
            var results = await _context.Word
     .Where(w => w.word == word)
     .Select(w => new SearchResult
     {
         URL = w.PageInfo.URL,
         PageRank = w.PageInfo.PageRank,
         WordCount = w.Count
     })
     .OrderByDescending(r => r.PageRank)
     .ThenByDescending(r => r.WordCount)
     .ToListAsync();
            return results;
        }
    }
}
