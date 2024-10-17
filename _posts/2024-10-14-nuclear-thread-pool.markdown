---
layout: post
title:  "Nuclear thread pool"
date:   2024-10-14 9:00:00 +0300
categories: jvm
---

&nbsp;&nbsp;&nbsp;&nbsp; Java developers know, that beneath classes from `*.concurrent.*` package there is a more low-level [atomic Compare-And-Swap (CAS) mechanism](https://medium.com/@satyendra.jaiswal/unlocking-performance-exploring-the-power-of-compare-and-swap-cas-operations-in-non-blocking-5c083978dc27).  
&nbsp;&nbsp;&nbsp;&nbsp; Let's take a look into `ReentrantLock.tryLock()` method: 
{%highlight java%}
final boolean tryLock() {
Thread current = Thread.currentThread();
int c = getState();
if (c == 0) {
  if (compareAndSetState(0, 1)) {
    setExclusiveOwnerThread(current);
    return true;
  }
} else
{% endhighlight %}  
&nbsp;&nbsp;&nbsp;&nbsp; Indeed, in main branch which returns `true` we see `compareAndSetState()` method, and if we follow stack of calls, we'll finish in `compareAndSetInt()` from `Unsafe` class.  
I won't look through all locks in `*.concurrent.*` package, but there are plenty of other places where `CAS` is used, you can find them easily.  
&nbsp;&nbsp;&nbsp;&nbsp; Now I take a step above and look into `LinkedBlockingQueue` and `ConcurrentLinkedQueue` collections.  
In `LinkedBlockingQueue` `offer()` and `take()` methods are using `ReentrantLock`. Are there other collections which are not using locks?  
&nbsp;&nbsp;&nbsp;&nbsp; Yes, sure. In `ConcurrentLinkedQueue` `offer()` and `take()` methods are based on atomic `compareAndSet()` method from `VarHandle` class (which does the same as `Unsafe.compareAndSet()`). That means, that, probably, `ReentrantLock` as a locking wrapper has some performance impact if compared with its atomic equivalent. The question is: how to measure this impact?  
&nbsp;&nbsp;&nbsp;&nbsp; I've implemented two thread-pools:  
- [ConcurrentLinkedQueuePool](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/main/benchmarks/src/main/kotlin/multithreading/threadpool/ConcurrentLinkedQueuePool.kt)
- [LinkedBlockingQueueThreadPool](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/main/benchmarks/src/main/kotlin/multithreading/threadpool/LinkedBlockingQueuePool.kt).

&nbsp;&nbsp;&nbsp;&nbsp; Both thread-pools contain list of [PoolRunnable](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/main/benchmarks/src/main/kotlin/multithreading/threadpool/PoolRunnable.kt) worker threads which are constantly monitoring `private val workingQueue` and if new task submitted by `execute()` method - takes it into work.  
&nbsp;&nbsp;&nbsp;&nbsp; In order to highlight performance impact of locking mechanism I'll submit a large number of light-weight tasks. Each task increments a counter and that's it. This approach should cause large amount of lock/unlock operations in `offer()/take()` method in `LinkedBlockingQueue` hence performance impact will become visible.
{% highlight java%}
  @Benchmark
  fun atomic() {
  val concurrentLinkedQueuePool = ConcurrentLinkedQueuePool(10)
  val counter = AtomicInteger()

        for (i in 0 until numOfTasks) {
            val t = Runnable {
                counter.getAndIncrement()
            }
            concurrentLinkedQueuePool.execute(t)
        }
        Thread.sleep(1)
        concurrentLinkedQueuePool.stop()
  }
{% endhighlight %}  
[Full code of the benchmark is here](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/main/benchmarks/src/main/kotlin/multithreading/threadpool/ThreadPoolBenchMark.kt).  
Let's run benchmark and see the numbers.
```
main summary:
Benchmark                   (numOfTasks)  Mode  Cnt      Score  ...  Units
ThreadPoolBenchMark.atomic     100000000  avgt    3  15677.358  ...  ms/op
ThreadPoolBenchMark.blocking   100000000  avgt    3  21440.026  ...  ms/op
```
&nbsp;&nbsp;&nbsp;&nbsp; Hypothesis was correct: atomic implementation is faster by ~25%.  
So, I think, this can be taken into consideration while solving multithreading problems.  
&nbsp;&nbsp;&nbsp;&nbsp; Stay atomic!

