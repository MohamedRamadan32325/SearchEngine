using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace WebPage.Migrations
{
    /// <inheritdoc />
    public partial class fo : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "Word",
                table: "Word",
                newName: "word");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "word",
                table: "Word",
                newName: "Word");
        }
    }
}
