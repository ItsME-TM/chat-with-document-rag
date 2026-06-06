using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
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
        private readonly HttpClient _httpClient;
        private readonly string _pythonServiceUrl;

        public AiService(HttpClient httpClient)
        {
            _httpClient = httpClient;
            // In a real app, this would come from configuration
            _pythonServiceUrl = "http://localhost:8000";
        }

        public async Task<object> UploadFileAsync(IFormFile file)
        {
            try
            {
                using var content = new MultipartFormDataContent();
                using var fileStream = file.OpenReadStream();
                content.Add(new StreamContent(fileStream), "file", file.FileName);

                var response = await _httpClient.PostAsync($"{_pythonServiceUrl}/upload", content);
                response.EnsureSuccessStatusCode();

                var responseContent = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<object>(responseContent, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                })!;
            }
            catch (Exception ex)
            {
                // In case of error, return a fallback response
                return new { status = "error", message = $"Failed to upload file: {ex.Message}" };
            }
        }

        public async Task<object> AskQuestionAsync(string question)
        {
            try
            {
                var request = new { question };
                var json = JsonSerializer.Serialize(request);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync($"{_pythonServiceUrl}/ask", content);
                response.EnsureSuccessStatusCode();

                var responseContent = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<object>(responseContent, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                })!;
            }
            catch (Exception ex)
            {
                // In case of error, return a fallback response
                return new { answer = $"Sorry, I encountered an error: {ex.Message}" };
            }
        }
    }
}