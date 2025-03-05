def test_run_interactions(self, device) -> None:
    device.get_mapped_element('svg').action(Actions.CLICK)
	device.get_mapped_element('Events').action(Actions.CLICK)
	device.get_mapped_element('Favorites').action(Actions.CLICK)


