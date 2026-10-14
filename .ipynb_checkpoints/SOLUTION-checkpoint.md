
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