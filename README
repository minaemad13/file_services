# File Service

This project is a Django-based application that allows users to upload files and perform various operations on the uploaded files. The application provides API endpoints to interact with the files and retrieve specific information.

## Getting Started

To set up the project locally, follow these instructions:

1. Clone the repository:

git clone https://github.com/minaemad13/file_services.git

2. Navigate to the project directory:
cd file_services

3. Install the required dependencies. It is recommended to use a virtual environment for isolation:
pip install -r requirements.txt

4. Run the Django development server:
python manage.py runserver

You should now have the project up and running locally.

## API Endpoints

### `POST /upload`

This endpoint allows users to upload files to the server. The file should be sent as a multipart form-data request.

#### Request

- Method: `POST`
- Endpoint: `/upload`
- Headers:
  - Content-Type: multipart/form-data
- Body:
  - file: The file to be uploaded

#### Response

If the file upload is successful, the endpoint will respond with a JSON object containing the file information.

Example response:

```json
{
  "result": {
    "id": 1,
    "filename": "example.txt"
  }
}
```
### `GET /get-one-random-line`

This endpoint retrieves a random line from a randomly selected uploaded file. The response format is determined by the Accept header.

#### Request

- Method: `GET`
- Endpoint: `/get-one-random-line`
- Headers:
  - Accept: application/json (or application/xml, text/plain, or any other supported format)

#### Response
The response format depends on the Accept header provided in the request.

If Accept: application/json:
Example response:

```json
{
  "line": "This is a random line."
}
```
If Accept: application/xml:
Example response:
<response>
  <line>This is a random line.</line>
</response>

If Accept: application/*:
Example response:
```json
{
  "line_number": 5,
  "file_name": "example.txt",
  "most_common_letter": "e",
  "line": "This is a random line."
}
```
If Accept: text/plain or no Accept header provided:
Example response:

This is a random line.

### `GET /get-one-random-line-backword`

This endpoint retrieves a random line from a randomly selected uploaded file and returns the line in reverse order.

#### Request

- Method: `GET`
- Endpoint: `get-one-random-line-backword/`

#### Response

The endpoint responds with a JSON object containing the reversed line, line number, and file name.

Example response:

```json
{
  "line_backword": ".enil modnar a si sihT",
  "line_number": 5,
  "file_name": "example.txt"
}
```
### `GET /get-requested-backword`

This endpoint retrieves a requested line number from a randomly selected uploaded file and returns the line in reverse order. The line number should be provided as a query parameter.

#### Request

- Method: `GET`
- Endpoint: `get-requested-backword/`
- body:
```json
{
    "line_number":5
}
```
#### Response

The endpoint responds with a JSON object containing the reversed line, line number, and file name.

Example response:

```json
{
  "line_backward": ".enil modnar a si sihT",
  "line_number": 5,
  "file_name": "example.txt"
}
```
### `GET /longest-100-lines`

This endpoint retrieves the 100 longest lines from all the uploaded files. The lines are sorted based on their length in descending order.

#### Request

- Method: `GET`
- Endpoint: `longest-100-lines/`

#### Response

The endpoint responds with a JSON object containing the 100 longest lines.

Example response:

```json
{
  "longest_100_lines": [
    "This is the longest line in the file.",
    "This line is also very long.",
  ]
}
```
### `GET /longest-20-lines`

This endpoint retrieves the 20 longest lines from a randomly selected uploaded file. The lines are sorted based on their length in descending order.

#### Request

- Method: `GET`
- Endpoint: `longest-20-lines/`

#### Response

The endpoint responds with a JSON object containing the 20 longest lines from the selected file.

Example response:

```json
{
  "longest_20_lines": [
    "This is the longest line in the file.",
    "This line is also very long.",
    ...
  ]
}
```