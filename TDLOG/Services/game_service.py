import sqlalchemy
from sqlalchemy import select
from Model.game import Game
from Model.player import Player
from Model.vessel import Vessel
from Model.weapon import Weapon
from Model.battlefield import Battlefield
from dao.game_dao import GameDao,GameEntity,PlayerEntity,VesselEntity,BattlefieldEntity,WeaponEntity

class GameService:
    def __init__(self):
        self.game_dao = GameDao()
    def create_game(self, player_name: str, min_x: int, max_x: int, min_y: int,
        max_y: int, min_z: int, max_z: int) -> int:
        game = Game()
        battle_field = Battlefield(min_x, max_x, min_y, max_y, min_z, max_z)
        game.add_player(Player(player_name, battle_field))
        return self.game_dao.create_game(game)
    def join_game(self, game_id: int, player_name: str) -> bool:
        game = self.game_dao.find_game(game_id)
        battlefield = Battlefield(-10,10,-10,10,-1,1)
        player = Player(player_name, battlefield)
        game.add_player(player)
    def get_game(self, game_id: int) -> Game:
        game = self.game_dao.find_game(game_id)
        return game

    def add_vessel(self, game_id: int, player_name: str, vessel_type: str,x: int, y: int, z: int) -> bool:
        game = self.game_dao.find_game(game_id)
        vessel = vessel_type(x, y, z)
        for player in game.get_players:
            if player.get_name() == player_name:
                battlefield = player.get_battlefield()
                battlefield.add_vessel(vessel)
                if vessel in battlefield.get_vessels():
                    stmt = select(PlayerEntity).where(PlayerEntity.name == player_name and PlayerEntity.game_id == game_id)
                    player_entity = self.db_session.scalars(stmt).one()
                    stmt = select(Battlefield).where(Battlefield.player_id == player_entity.id)
                    battlefield_entity = self.db_session.scalars(stmt).one()
                    self.game_dao.create_vessel(battlefield_entity.id, vessel)
                    return True
                else:
                    return False


        
    def shoot_at(self, game_id: int, shooter_name: str, vessel_id: int, x: int,y: int, z: int) -> bool:
        game = self.game_dao.find_game(game_id)
        vessel = self.game_dao.find_vessel(vessel_id)
        if vessel.weapon.ammunitions >= 1:
            stmt = update(WeaponEntity).where(WeaponEntity.vessel_id == vessel_id).values({WeaponEntity.ammunitions: WeaponEntity.ammunitions - 1})
            self.db_session.scalars(stmt).one()
            for player in game.get_players():
                if player.get_name() == shooter_name:
                    battlefield = player.get_battlefield()
                    for vessels in battlefield.get_vessels():
                        if vessels == vessel:
                            vessels.fire_at(x, y, z)
                            stmt = update(VesselEntity).where(VesselEntity.coord_x == x, VesselEntity.coord_y == y, VesselEntity.coord_z == z).values({VesselEntity.hits_to_be_destroyed: VesselEntity.hits_to_be_destroyed - 1})
                            self.db_session.scalars(stmt).one()
                            return True
                        return False


    def get_game_status(self, game_id: int, shooter_name: str) -> str:
        game = self.game_dao.find_game(game_id)
        for player in game.get_players():
            if player.get_name() == shooter_name:
                if player.get_battlefield().get_vessels() == []:
                    return "PERDU"
            elif player.get_battlefield().get_vessels() == []:
                return "GAGNE"
        return "ENCOURS"
