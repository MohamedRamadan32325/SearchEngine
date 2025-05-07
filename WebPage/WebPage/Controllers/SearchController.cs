using Microsoft.AspNetCore.Mvc;
using WebPage.Repositry.IRepositry;

namespace WebPage.Controllers
{
    public class SearchController : Controller
    {
        private readonly ISearchService _searchService;

        public SearchController(ISearchService searchService)
        {
            _searchService = searchService;
        }

        public IActionResult Index()
        {
            return View();
        }

        [HttpGet]
        public async Task<IActionResult> Search(string query)
        {
            if (string.IsNullOrEmpty(query))
            {
                return View("Index");
            }

            var results = await _searchService.SearchAsync(query);
            return View("Index", results);
        }
    }
}
