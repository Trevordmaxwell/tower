import time
import random

class Enemy:
    """Basic enemy that walks along the path."""
    def __init__(self, health: int, speed: int = 1):
        self.health = health
        self.speed = speed
        self.position = 0

    def move(self) -> None:
        self.position += self.speed

    def is_alive(self) -> bool:
        return self.health > 0


class FastEnemy(Enemy):
    """Enemy that moves faster but has less health."""
    def __init__(self):
        super().__init__(health=2, speed=2)


class Tower:
    """Simple tower that shoots the first enemy in range each tick."""
    def __init__(self, position: int, damage: int = 1, rng: int = 1):
        self.position = position
        self.damage = damage
        self.range = rng

    def attack(self, enemies: list[Enemy]) -> None:
        for enemy in enemies:
            if enemy.is_alive() and abs(enemy.position - self.position) <= self.range:
                enemy.health -= self.damage
                print(
                    f"Tower at {self.position} hits enemy at {enemy.position} for {self.damage} damage."
                )
                break


class Game:
    def __init__(self, path_length: int = 10):
        self.path_length = path_length
        self.towers: list[Tower] = []
        self.enemies: list[Enemy] = []
        self.tick = 0

    def add_tower(self, tower: Tower) -> None:
        self.towers.append(tower)

    def spawn_enemy(self, enemy: Enemy) -> None:
        self.enemies.append(enemy)

    def step(self) -> bool:
        """Advance the game by one tick.

        Returns False if the game ends either by losing or winning.
        """
        self.tick += 1
        print(f"\n--- Tick {self.tick} ---")
        for enemy in list(self.enemies):
            enemy.move()
            if enemy.position >= self.path_length:
                print("An enemy reached the end. Game over!")
                return False
        for tower in self.towers:
            tower.attack(self.enemies)
        # Remove defeated enemies
        self.enemies = [e for e in self.enemies if e.is_alive()]
        if not self.enemies:
            print("All enemies defeated. You win!")
            return False
        return True

    def run(self) -> None:
        while self.enemies and self.step():
            time.sleep(0.5)


def main() -> None:
    game = Game(path_length=12)
    # Place a couple of towers
    game.add_tower(Tower(position=4, damage=2))
    game.add_tower(Tower(position=8, damage=1))

    # Spawn a mix of basic and fast enemies
    for _ in range(3):
        game.spawn_enemy(Enemy(health=3))
    for _ in range(2):
        game.spawn_enemy(FastEnemy())

    game.run()


if __name__ == "__main__":
    main()
