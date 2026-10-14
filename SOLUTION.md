
|  Method 	| Local  	| Same-Zone  	|  Different Region 	|
|---	|---	|---	|---	|---	|
|   REST add	|   2.416	|   3.330	|   410.148	|
|   gRPC add	|   0.766	|   1.421	|   164.930 	|
|   REST rawimg	|   4.924	|   7.834	|   1267.757	|
|   gRPC rawimg	|  12.859   |   15.575	|   209.369	|
|   REST dotproduct	|   2.835	|   4.114	|   314.226	|
|   gRPC dotproduct	|   0.851	|   1.215	|   183.124 	|
|   REST jsonimg	|  27.250	|   32.526	|   1487.469	|
|   gRPC jsonimg	|  27.639   |   31.017	|   228.373	|
|   PING        |   0.036    |   0.427   |   159.318    |

You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.

## My Analysis
Based on my findings, gRPC generally performed better than REST. This is emphasized through all the timings when the virutual machines are in different zones. When running locally or in the same zone, the peformance of the REST and gRPC are pretty much the same. This totally makes sense because of the role that network latency has. Since REST establishes a new TCP connection with each request while gRPC reuses a single TCP connection for multiple requests, the location of the server and client determine the performance of the communication. If the zones for the client and server are different then that means that for the REST a single request takes 159.318 ms which for 100 requests is a lot of time while gRPC establishes the TPC connection and then the rest of the requests which takes 159.318 plus however long the rest of the requests take to process. As a result, gRPC is going to be much faster. While local and same zone communication between the client and server will be similar since the ping is much less between requests. Now I know if I am going to build an application with users from all over and I have a client and server, gRPC is the way to go. 