using Microsoft.EntityFrameworkCore;
using WebPage.Models;

namespace WebPage.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext>options) : base(options) { }
        public DbSet<inverted_index_sorted> Word { get; set; }
        public DbSet<Urlswithranks> PageInfos { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<inverted_index_sorted>(entity =>
            {
                entity.HasKey(w => new { w.word, w.FileName });

                entity.HasOne(w => w.PageInfo)
                    .WithMany(p => p.WordIndices)
                    .HasForeignKey(w => w.FileName)
                    .HasPrincipalKey(p => p.FileName);
            });

            modelBuilder.Entity<Urlswithranks>()
                .HasKey(p => p.FileName);
        }

    }
}
