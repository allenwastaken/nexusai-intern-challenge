import asyncio
import random
import time
from dataclasses import dataclass

async def fetch_crm(phone):
    start = time.perf_counter()
    await asyncio.sleep(random.uniform(0.2, 0.4))
    elapsed = (time.perf_counter() - start) * 1000
    print(f"CRM fetch took: {elapsed:.2f}ms")
    return {"name": "Allen", "phone": phone}

async def fetch_bill(phone):
    start=time.perf_counter()
    await asyncio.sleep(random.uniform(0.15, 0.35))
    if random.random() < 0.1:
        raise TimeoutError("Billing system timed out")
    elapsed = (time.perf_counter() - start) * 1000
    print(f"Bill fetch took: {elapsed:.2f}ms")
    return {"phone": phone, "billing_status": "paid"}

async def fetch_history(phone):
    start=time.perf_counter()
    await asyncio.sleep(random.uniform(0.1,0.3))
    elapsed = (time.perf_counter() - start) * 1000
    print(f"History fetch took: {elapsed:.2f}ms")
    return{"phone":phone, "tickets":["wrong plan activated","cancellation request","billing overcharge","service outage","login issue"]}

async def fetch_sequential(phone):
    start=time.perf_counter()
    crm=await fetch_crm(phone)
    bill=await fetch_bill(phone)
    history=await fetch_history(phone)
    end=time.perf_counter()
    elapsed=(end-start)*1000 #ms conversion
    print(f"Sequential time taken: {elapsed:.2f} ms")
    return crm, bill, history

async def fetch_parallel(phone):
    start=time.perf_counter()
    crm, bill, history= await asyncio.gather(
        fetch_crm(phone),
        fetch_bill(phone),
        fetch_history(phone),
        return_exceptions=True
    )
    if isinstance(bill, Exception):
        print("WARNING: Billing fetch failed")
        bill = None
    end=time.perf_counter()
    elapsed=(end-start)*1000 #ms conversion
    print(f"Parallel time taken: {elapsed:.2f} ms")
    context = build_context(crm, bill, history, elapsed)
    return context

@dataclass
class CustomerContext:
    phone: str
    name: str
    billing_status: str
    tickets: list
    data_complete: bool      # False if any fetch returned None
    fetch_time_ms: float     # elapsed time from parallel fetch
    
def build_context(crm, bill, history, elapsed):
    data_complete = not any(x is None for x in [crm, bill, history])
    
    return CustomerContext(
        phone=crm["phone"],
        name=crm["name"],
        billing_status=bill["billing_status"] if bill is not None else None,
        tickets=history["tickets"],
        data_complete=data_complete,
        fetch_time_ms=elapsed   
    )

if __name__ == "__main__":
    try:
        asyncio.run(fetch_sequential("123-456-7890"))
    except TimeoutError as e:
        print(f"Sequential failed: {e}")

    context = asyncio.run(fetch_parallel("123-456-7890"))
    print(context)
