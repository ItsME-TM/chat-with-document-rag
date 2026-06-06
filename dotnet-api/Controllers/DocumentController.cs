using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;

namespace dotnet_api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
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
            // In Phase 1, we return a fixed response. In Phase 2, we'll call the Python service.
            var result = await _aiService.UploadFileAsync(file);
            return Ok(result);
        }

        [HttpPost("ask")]
        public async Task<IActionResult> Ask([FromBody] QuestionRequest request)
        {
            // In Phase 1, we return a fixed response. In Phase 2, we'll call the Python service.
            var result = await _aiService.AskQuestionAsync(request.Question);
            return Ok(result);
        }
    }

    public class QuestionRequest
    {
        public string Question { get; set; }
    }

    public class UploadResponse
    {
        public string Status { get; set; }
        public string Message { get; set; }
    }

    public class AskResponse
    {
        public string Answer { get; set; }
    }
}