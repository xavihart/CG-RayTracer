# CG-RayTracer
(Personal practising) 

implementation of “Ray Tracing in one Weekend“ by ___Peter Shirley___ 

## Depend on libs as follows:

- `Python3`, ` numpy`, `opencv`, `multiprocessing`, `sys`, `tqdm`

## Properties:

- in infant stage, bug exists maybe
- naive-multiprocessing

## Multiprocessing-Strategy

- assumption : Dividing the image into blocks may be unbalanced for processes, since pixels with high computational complexity is always clustering.
- implementation : We simple choose randomly permutated pixel arrays as blocks to balance the work for each process.
- to do : Maybe we can first tracing rays in a relatively small image for specific scenes with low computational cost, then we get the map for computational complexity(timeCMD), according to which we can scale up the map into normal size to assign pixels to each process. 

##  Run

```
python ./main.py --ns [ns] --r [resolution] --name [file-name] --multithread [on or off] --block-num [process number]
```



## Working Flows

:white_check_mark: First Week

> :white_check_mark: Preparations, basic headers
>
> :white_check_mark: Sphere and object list
>
> :white_check_mark: Antialiasing
>
> :white_check_mark: Materials(lambertian, metal, dielectric)
>
> :white_check_mark: Reflection and refraction
>
> :white_check_mark: Camera position and blur

:white_circle: Next Week

>
>
>:white_check_mark: Moving sphere
>
>:white_check_mark: BVH speed-up
>
>:white_check_mark: Textures
>
>:white_check_mark:  Perlin noise
>
>:white_check_mark: Texture mapping
>
>:white_check_mark: Rectangles and lights
>
>:white_circle: Instances and volumes 



Snaps:
<img src="./0001.jpg" alt="0002" style="zoom: 25%;" />

<img src="./0002.jpg" alt="0002" style="zoom: 25%;" />
