using Microsoft.EntityFrameworkCore;
using WebPage.Data;
using WebPage.Repositry;
using WebPage.Repositry.IRepositry;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
var connectionsttring = builder.Configuration.GetConnectionString("Default") ?? 
    throw new InvalidOperationException("NO Connection String");
builder.Services.AddControllersWithViews();
builder.Services.AddDbContext<AppDbContext>(options=>options.UseSqlServer(connectionsttring));
builder.Services.AddScoped<ISearchService, SearchService>();
var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Search}/{action=Index}/{id?}");

app.Run();
 