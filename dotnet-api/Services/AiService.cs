using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;

namespace dotnet_api.Services
{
    public interface IAiService
    {
        Task<object> UploadFileAsync(IFormFile file);
        Task<object> AskQuestionAsync(string question);
    }

    public class AiService : IAiService
    {
        public Task<object> UploadFileAsync(IFormFile file)
        {
            // In Phase 1, return a fixed response.
            return Task.FromResult<object>(new { status = "success", message = "File received" });
        }

        public Task<object> AskQuestionAsync(string question)
        {
            // In Phase 1, return a fixed response.
            return Task.FromResult<object>(new { answer = "This is a skeleton response." });
        }
    }
}