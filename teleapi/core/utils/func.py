def pass_additional_kwargs(obj, **additional_kwargs):
    async def wrapper(*args, **kwargs):
        return await obj(*args, **kwargs, **additional_kwargs)

    return wrapper
