---
layout: post
title:  "Default hashCode(): OutOfMemory"
date:   2023-05-03 18:42:07 +0300
categories: jvm
---
&nbsp;&nbsp; No, this post is not about getting OutOfMemoryError during `hashCode` call, as you might think :-).  
&nbsp;&nbsp; Recently I was asked a question during the interview: "What's the default implementation of hashCode()?"  
&nbsp;&nbsp; Correct answer (according to interviewer) was: "By default, JVM uses address of object in memory for creating hash"  
Right? No.  
[Let's jump in](https://github.com/openjdk/jdk/blob/master/src/hotspot/share/runtime/synchronizer.cpp#L917).  
&nbsp;&nbsp; Here is a sample from JVM `synchronizer.cpp`. Notice, that if object has no hash, method `get_next_hash(current, obj)` is called.
{% highlight java %}
if (hash == 0) {                        // if it does not have a hash
hash = get_next_hash(current, obj);  // get a new hash
temp = mark.copy_set_hash(hash)   ;  // merge the hash into header
assert(temp.is_neutral(), "invariant: header=" INTPTR_FORMAT, temp.value());
uintptr_t v = Atomic::cmpxchg((volatile uintptr_t*)monitor->header_addr(), mark.value(), temp.value());
{% endhighlight %}  
&nbsp;&nbsp; Inside of this method we see this:  

{% highlight java %}
// hashCode() generation :
//
// Possibilities:
// * MD5Digest of {obj,stw_random}
// * CRC32 of {obj,stw_random} or any linear-feedback shift register function.
// * A DES- or AES-style SBox[] mechanism
// * One of the Phi-based schemes, such as:
//   2654435761 = 2^32 * Phi (golden ratio)
//   HashCodeValue = ((uintptr_t(obj) >> 3) * 2654435761) ^ GVars.stw_random ;
// * A variation of Marsaglia's shift-xor RNG scheme.
// * (obj ^ stw_random) is appealing, but can result
//   in undesirable regularity in the hashCode values of adjacent objects
//   (objects allocated back-to-back, in particular).  This could potentially
//   result in hashtable collisions and reduced hashtable efficiency.
//   There are simple ways to "diffuse" the middle address bits over the
//   generated hashCode values:

static inline intptr_t get_next_hash(Thread* current, oop obj) {
intptr_t value = 0;
if (hashCode == 0) {
// This form uses global Park-Miller RNG.
// On MP system we'll have lots of RW access to a global, so the
// mechanism induces lots of coherency traffic.
value = os::random();
} else if (hashCode == 1) {
// This variation has the property of being stable (idempotent)
// between STW operations.  This can be useful in some of the 1-0
// synchronization schemes.
intptr_t addr_bits = cast_from_oop<intptr_t>(obj) >> 3;
value = addr_bits ^ (addr_bits >> 5) ^ GVars.stw_random;
} else if (hashCode == 2) {
value = 1;            // for sensitivity testing
} else if (hashCode == 3) {
value = ++GVars.hc_sequence;
} else if (hashCode == 4) {
value = cast_from_oop<intptr_t>(obj);
} else {
// Marsaglia's xor-shift scheme with thread-specific state
// This is probably the best overall implementation -- we'll
// likely make this the default in future releases.
unsigned t = current->_hashStateX;
t ^= (t << 11);
current->_hashStateX = current->_hashStateY;
current->_hashStateY = current->_hashStateZ;
current->_hashStateZ = current->_hashStateW;
unsigned v = current->_hashStateW;
v = (v ^ (v >> 19)) ^ (t ^ (t >> 8));
current->_hashStateW = v;
value = v;
}

value &= markWord::hash_mask;
if (value == 0) value = 0xBAD;
assert(value != markWord::no_hash, "invariant");
return value;
}
{% endhighlight %}  
&nbsp;&nbsp; Going ahead and using other available on-topic guides ([like this](https://shipilev.net/jvm/anatomy-quarks/26-identity-hash-code/), as I'm not C++ guy), we see that  
ONLY if `hashCode == 4` (it stands for JVM option `-XX:hashCode=4`) internal memory address is used.  
So, indeed, `hashCode` is OutOfMemory, at least in 3/4 cases.  
&nbsp;&nbsp; Happy interviews :-) and do not hesitate to show people JVM sources, if needed.