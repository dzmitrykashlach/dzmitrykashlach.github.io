---
layout: post
title:  "Kotlin coroutines: asynchronous maneuvers"
date:   2023-05-12 00:00:07 +0300
categories: kotlin
---
&nbsp;&nbsp; So, I have some experience with Kotlin coroutines, but let's call my level, hm, not too deep.  
[This article](https://medium.com/mobilepeople/kotlin-coroutine-dispatchers-overview-f8000a6037f4) inspired me for doing some experiment:
> Dispatchers.IO  
> This dispatcher is like Default but has a bigger parallelism limit. 
> It uses the same thread pool under the hood but can dedicate more threads for coroutines execution. 
> IO dispatcher, as mean its name, is useful for blocking input/output operations, but do not use it for CPU-heavy operations:  
> large parallelism may lead to parallel work of a lot of threads, and switching between them also kills your performance.

&nbsp;&nbsp; First, what are dispatchers which are mentioned above? Here is link to [Kotlin documentation](https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html#dispatchers-and-threads) and [CoroutineDispatcher abstract class](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-dispatcher/).  
In short, dispatcher  
> determines what thread or threads the corresponding coroutine uses for its execution

__Idea__  
&nbsp;&nbsp; The question is: what will happen if I violate recommendation from above and use `Dispatchers.IO` for CPU-intensive calculations?  
&nbsp;&nbsp; [I've created benchmark](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/main/benchmarks/src/main/kotlin/coroutines/DispatchersCPUBenchMark.kt), which calculates factorial and I'm running it using `var nCoroutines = 4000` 3 times: with plain threads,  
with `Dispatchers.Default`, with `Dispatchers.IO`  

__Results__  

```
main summary:
Benchmark                                             (factorialSize)  Mode  Cnt        Score        Error  Units
DispatchersCPUBenchMark.coroutinesDispatchersDefault             2000  avgt    3     5255.348 ±  75191.476  us/op
DispatchersCPUBenchMark.coroutinesDispatchersDefault             4000  avgt    3     3813.471 ±  33133.584  us/op
DispatchersCPUBenchMark.coroutinesDispatchersIO                  2000  avgt    3     6437.317 ±  12881.315  us/op
DispatchersCPUBenchMark.coroutinesDispatchersIO                  4000  avgt    3     9983.775 ±  27035.014  us/op
DispatchersCPUBenchMark.threads                                  2000  avgt    3  1732705.383 ± 355342.356  us/op
DispatchersCPUBenchMark.threads                                  4000  avgt    3  6034969.050 ± 664852.667  us/op 
```

|                 | plain threads             | coroutinesDispatchersDefault | coroutinesDispatchersIO |
|-----------------|---------------------------|------------------------------|-------------------------|
| CPU, %          | 100                       | 100                          | 100                     |
| Memory, %       | 40                        | 64                           | 64                      |
| Runtime, millis | 1641755.324 - 6028442.417 | 5617.26 - 7342.059 | 13205.202 - 5070.477 |

&nbsp;&nbsp; Benchmark summary looks quite logical: `threads` show maximum running time and `coroutinesDispatchersIO` performs slower than `coroutinesDispatchersDefault`.

&nbsp;&nbsp;BUT...  
* Performance monitor reported that plain threads take the least amount of memory while it's declared that coroutines are light-weight.  
* When I increase load (from `factorialSize = 2000` to `factorialSize = 4000`) running time for `coroutinesDispatchersDefault` goes down from `5355.348 millis` to `3813.471 millis`.
* Running times of different iterations for `coroutinesDispatchersDefault` vary a lot:
```
main: coroutines.DispatchersCPUBenchMark.coroutinesDispatchersDefault | factorialSize=2000
Warm-up 1: 2170.449 us/op
Iteration 1: 4014.905 us/op
Iteration 2: 1896.534 us/op
Iteration 3: 9854.606 us/op
```  
&nbsp;&nbsp; You can notice that `Iteration 2` ended faster than `Iteration 1` but `Iteration 3` took even longer time.  
The same picture (different running time for particular iteration) is for `coroutinesDispatchersIO` but deviation is not so huge (see results below).  
```  
main: coroutines.DispatchersCPUBenchMark.coroutinesDispatchersIO | factorialSize=2000
Warm-up 1: 5923.528 us/op
Iteration 1: 5426.481 us/op
Iteration 2: 28599.197 us/op
Iteration 3: 5589.929 us/op
```

__Conclusion__  
&nbsp;&nbsp; While Kotlin documentation looks correct, benchmark highlighted few things, which look like an anomaly and deserve additional testing.  
I'll follow up them later...
