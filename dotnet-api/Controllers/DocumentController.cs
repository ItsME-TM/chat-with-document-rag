using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using dotnet_api.Services;

namespace dotnet_api.Controllers
{
    [ApiController]
    [Route("api")]
    public class DocumentController : ControllerBase
    {
        private readonly IAiService _aiService;

        public DocumentController(IAiService aiService)
        {
            _aiService = aiService;
        }

        [HttpPost("upload")]
        public async Task<IActionResult> Upload(IFormFile file)
        {
            // Forward request to Python service
            var result = await _aiService.UploadFileAsync(file);
            return Ok(result);
        }

        [HttpPost("ask")]
        public async Task<IActionResult> Ask([FromBody] QuestionRequest request)
        {
            // Forward request to Python service
            var result = await _aiService.AskQuestionAsync(request.Question);
            return Ok(result);
        }
    }

    public class QuestionRequest
    {
        public string Question { get; set; } = string.Empty;
    }

    public class UploadResponse
    {
        public string Status { get; set; } = string.Empty;
        public string Message { get; set; } = string.Empty;
    }

    public class AskResponse
    {
        public string Answer { get; set; } = string.Empty;
    }
}