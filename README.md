# Flask with REST APIs

### Objectives

The 888Spectate API provides endpoints for managing sports, events, and selections within a sportsbook product. The API supports creating, retrieving, updating, and deleting these entities, ensuring consistency by automatically deactivating events and sports when all their selections or events are inactive, respectively.

### CSRF Protection

- CSRF Token generation with session token for 5 minutes. 
- Generate token first before making any non-GET method. Use "/get_csrf_token" url to get the token.
- Use this token in request headers with POST requests.

### Database System

The API uses SQLite as its persistent storage. The following entity relationships exist:

Sport: Contains multiple events.
Event: Contains multiple selections and belongs to a sport.
Selection: Belongs to an event.

The schema is defined as follows:

![Screenshot](https://github.com/NikhilSalv/888_Spectate_Task/blob/main/Screenshots/Screenshot%202024-06-11%20at%2009.47.54.png)

### Database :

<table>
  <tr>
    <td>
      <img src="https://github.com/NikhilSalv/888_Spectate_Task/blob/main/Screenshots/Screenshot%202024-06-11%20at%2009.51.16.png" width="500" alt="AWS Certification">
    </td>
    <td>
      <img src="https://github.com/NikhilSalv/888_Spectate_Task/blob/main/Screenshots/Screenshot%202024-06-11%20at%2009.51.24.png" width="500" alt="AWS Certification">
    </td>
    <td>
      <img src="https://github.com/NikhilSalv/888_Spectate_Task/blob/main/Screenshots/Screenshot%202024-06-11%20at%2009.51.34.png" width="500" alt="AWS Certification">
    </td>
  </tr>
</table>

### REST APIs
##### 1. Create Data

<u>Endpoint: POST /create</u>


Description: Creates a new sport, event, or selection.
Request Headers: Content-Type: application/json

Request Body Example (Sport, events and selections):

<table>
  <tr>
    <td>
      <img src="https://github.com/NikhilSalv/888_Spectate_Task/blob/main/Screenshots/create%20sport.png" width="500" alt="AWS Certification">
    </td>
    <td>
      <img src="https://github.com/NikhilSalv/888_Spectate_Task/blob/main/Screenshots/create%20event.png" width="500" alt="AWS Certification">
    </td>
    <td>
      <img src="https://github.com/NikhilSalv/888_Spectate_Task/blob/main/Screenshots/create%20selection.png" width="500" alt="AWS Certification">
    </td>
  </tr>
</table>


##### 2. Update Data

<u>Endpoint: PUT /update/<string:type>/<int:id></u>


Description: Updates an existing sport, event, or selection.
Request Headers: Content-Type: application/json

Request Body Example  (Sport, events and selections):

<table>
  <tr>
    <td>
      <img src="https://github.com/NikhilSalv/888_Spectate_Task/blob/main/Screenshots/update%20sports.png" width="500" alt="AWS Certification">
    </td>
    <td>
      <img src="https://github.com/NikhilSalv/888_Spectate_Task/blob/main/Screenshots/update%20selections.png" width="500" alt="AWS Certification">
    </td>
    <td>
      <img src="https://github.com/NikhilSalv/888_Spectate_Task/blob/main/Screenshots/update%20selections.png" width="500" alt="AWS Certification">
    </td>
  </tr>
</table>


#### 3. Get Data

<u>Endpoint: GET /getdata</u>

- Description: Retrieves data for sports, events, or selections with filters.
- Request Headers: Content-Type: application/json
- Query Parameters Example:
-- For sports: ?type=sports&name=Football&active=true
-- For events: ?type=events&status=Pending&sport_id=1
-- For selections: ?type=selections&event_id=1
- Response: JSON array of the filtered entities.

#### 4. Get Data by Slug

Endpoint: GET /<string:type>/<string:slug>

Description: Retrieves a sport or event by its slug.
Request Headers: Content-Type: application/json

### Docker Setup

The Docker setup allows for easy deployment and local testing of the application. 
The Flask app runs on default port 5000. The Dockerfile exposes port 8080 to the host.

Dockerfile:

<img src="https://github.com/NikhilSalv/888_Spectate_Task/blob/main/Screenshots/Docker.png" width="700" alt="AWS Certification">

### Additional features : 

- CSRF Token generation with session token for 5 minutes. 

### Future Implementations  :

- Parameterized queries to prevent SQL Injection
- Caching to optimize queries
- Delete operation to delete record from any / all entities.

#### Conclusion

This documentation outlines the objectives, database schema, REST API endpoints, and Docker setup for the 888Spectate REST API. This setup allows for efficient management of sports, events, and selections within the sportsbook product, ensuring data integrity and ease of use.

#### Aknowledgement 

##### I have truly enjoyed developing this application. Thank you 888Spactate for giving me this opportunity. I am looking forward to contribute my best to the 888 Spectate.
