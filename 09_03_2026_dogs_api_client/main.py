import os
import requests
from enum import Enum
from typing import Optional, List, Set, Dict


class EntityState(Enum):
    UNCHANGED = 0
    NEW = 1
    MODIFIED = 2

class Dog:
    def __init__(self, breed: str, name: str, path: str = None):
        self.breed:str = breed
        self.name:str = name
        self.path: Optional[str] = path
        self.state = EntityState.UNCHANGED
        self._temp_image_data: Optional[bytes] = None

    def get_image(self) -> bytes:
        """Получает изображение из временного хранилища или с диска"""
        if self._temp_image_data is not None:
            return self._temp_image_data
        elif self.path and os.path.exists(self.path):
            with open(self.path, "rb") as image_file:
                return image_file.read()
        else:
            raise ValueError("No image")
    def set_image(self, img_data: bytes):
        """Устанавливает новое изображение"""
        self._temp_image_data = img_data
        if self.state == EntityState.UNCHANGED:
            self.state = EntityState.MODIFIED

    def mark_default_state(self):
        """Сброс состояния после сохранения изображения"""
        self.state = EntityState.UNCHANGED
        self._temp_image_data = None

    def __str__(self):
        return f"Breed: {self.breed}, Name: {self.name}"

    def __repr__(self):
        return f"Dog(breed='{self.breed}', name='{self.name}', path='{self.path}')"


class DogsApiClient:
    def __init__(self, api_url: str):
        self.url = api_url.strip()

    def _get_image_url(self) -> Optional[str]:
        try:
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("message") and data.get('status') == "success":
                img_link = data.get('message')
                return img_link
            else:
                return ''
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_dog_info(self, url: str):
        # https://images.dog.ceo/breeds/hound-afghan/n02088094_12664.jpg
        edited_url = url.strip().lstrip("https://").split("/")
        if len(edited_url) < 4:
            return None
        breed = edited_url[2]
        name = edited_url[3]
        return breed, name


    def get_image(self) -> Optional[dict]:
        if not self.url:
            return None
        try:
            image_url = self._get_image_url()
            if image_url is None:
                return None
            breed, name = self.get_dog_info(url=image_url)
            response = requests.get(image_url, timeout=5)
            response.raise_for_status()
            return {
                'breed': breed,
                'name': name,
                'img': response.content
            }
        except Exception as e:
            print(f"Error: {e}")
            return None

class DogImageContext:
    def __init__(self, data_path: str = "dogs-data", batch_size: int = 100):
        self.data_path: str = data_path
        self.batch_size: int = batch_size
        self.context: dict[str, List[Dog]] = {}
        self._tracked_changes: Set[Dog] = set()
        self._ensure_data_directory()
        self._load_data_from_disc()

    def _ensure_data_directory(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    def _load_data_from_disc(self):
        self.context.clear()
        if os.path.exists(self.data_path):
            for root, dirs, files in os.walk(self.data_path):
                if root != self.data_path:
                    breed = os.path.basename(root)
                    breed_dogs = []
                    for file in files:
                        if file.lower().endswith((".jpg", ".png", ".jpeg")):
                            dog = Dog(breed=breed, name=file, path=os.path.join(root, file))
                            dog.state = EntityState.UNCHANGED
                            breed_dogs.append(dog)
                    if breed_dogs:
                        self.context[breed] = breed_dogs

    def _find_dog(self, breed: str, name: str) -> Optional[Dog]:
        if breed in self.context:
            for dog in self.context[breed]:
                if dog.name == name:
                    return dog
        return None

    def add(self, breed: str, name: str, img: bytes) -> Dog:
        existing_dog = self._find_dog(breed, name)
        if existing_dog:
            existing_dog.set_image(img)
            self._tracked_changes.add(existing_dog)
            return existing_dog
        new_dog = Dog(breed=breed, name=name)
        new_dog.set_image(img)
        new_dog.state = EntityState.NEW

        if breed in self.context:
            self.context[breed].append(new_dog)
        else:
            self.context[breed] = [new_dog]

        self._tracked_changes.add(new_dog)

        if len(self.context[breed]) == self.batch_size:
            self.save_batch()

        return new_dog

    def save_batch(self):
        if not self._tracked_changes:
            return
        by_breed: Dict[str, List[Dog]] = {}
        for dog in self._tracked_changes:
            if dog.breed not in by_breed:
                by_breed[dog.breed] = []
            by_breed[dog.breed].append(dog)
        for breed, dogs in by_breed.items():
            breed_path = os.path.join(self.data_path, breed)
            if not os.path.exists(breed_path):
                os.makedirs(breed_path)
            for dog in dogs:
                if dog.state in [EntityState.NEW, EntityState.MODIFIED]:
                    file_path = os.path.join(breed_path, dog.name)
                    with open(file_path, "wb") as f:
                        f.write(dog.get_image())
                    dog.path = file_path
                    dog.mark_default_state()
        self._tracked_changes.clear()

    def save_all(self):
        self.save_batch()

    def discard_changes(self):
        for dog in list(self._tracked_changes):
            if dog.state == EntityState.NEW:
                if dog.breed in self.context:
                    if dog in self.context[dog.breed]:
                        self.context[dog.breed].remove(dog)
            elif dog.state == EntityState.MODIFIED:
                dog.mark_default_state()

        self._tracked_changes.clear()

    def get_dogs_by_breed(self, breed: str) -> List[Dog]:
        pass

    def get_all_dogs(self) -> List[Dog]:
        pass



class DogService:
    def __init__(self, client: DogsApiClient, data_context: DogImageContext ):
        self.client = client
        self.context = data_context

    def parse(self, img_count: int, batch_size: int = 100) -> List[Dog]:

        downloaded_dogs = []
        self.context.batch_size = batch_size

        for _ in range(img_count):
            dog_data = self.client.get_image()
            if dog_data is None:
                continue
            new_dog = self.context.add(breed=dog_data['breed'], name=dog_data['name'], img=dog_data['img'])
            downloaded_dogs.append(new_dog)

        return downloaded_dogs

    def save_changes(self):
        self.context.save_all()


class ServiceBuilder:
    def __init__(self, base_url:str, data_path:str):
        self.base_url = base_url
        self.data_path = data_path

    def get_dog_service(self) -> DogService:
        api_client = DogsApiClient(self.base_url)
        context = DogImageContext(self.data_path)
        return DogService(api_client, context)

if __name__ == "__main__":
    base_url = "https://dog.ceo/api/breeds/image/random"
    data_path = "dogs-data"
    service_builder = ServiceBuilder(base_url=base_url, data_path=data_path)
    dog_service = service_builder.get_dog_service()
    image = dog_service.parse(img_count=20)
    dog_service.save_changes()
